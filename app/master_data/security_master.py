from __future__ import annotations

from dataclasses import dataclass

from app.master_data.schemas import AssetMaster, CompanyMaster, EntityResolutionResult, IndicationMaster


@dataclass
class SecurityMasterStore:
    companies: dict[str, CompanyMaster]
    assets: dict[str, AssetMaster]
    indications: dict[str, IndicationMaster]


class SecurityMaster:
    def __init__(self, store: SecurityMasterStore | None = None) -> None:
        self.store = store or SecurityMasterStore(companies={}, assets={}, indications={})

    @staticmethod
    def _norm(text: str) -> str:
        return ''.join(ch for ch in text.lower() if ch.isalnum() or ch.isspace()).strip()

    def load_demo_records(self) -> None:
        self.store.companies = {
            'NBIX': CompanyMaster(company_id='cmp_nbix', ticker='NBIX', cik='0000795613', name='Neurocrine Biosciences', aliases=['Neurocrine', 'NBIX']),
            'SRPT': CompanyMaster(company_id='cmp_srpt', ticker='SRPT', cik='0000872539', name='Sarepta Therapeutics', aliases=['Sarepta', 'SRPT']),
        }
        self.store.assets = {
            'crinecerfont': AssetMaster(asset_id='ast_nbix_001', company_id='cmp_nbix', canonical_name='crinecerfont', aliases=['NBI-74788'], target='CRF1 receptor', modality='small_molecule'),
            'elevidys': AssetMaster(asset_id='ast_srpt_001', company_id='cmp_srpt', canonical_name='elevidys', aliases=['SRP-9001', 'delandistrogene moxeparvovec'], target='dystrophin', modality='gene_therapy'),
        }
        self.store.indications = {
            'ca_h': IndicationMaster(indication_id='ca_h', name='classic congenital adrenal hyperplasia', aliases=['CAH']),
            'dmd': IndicationMaster(indication_id='dmd', name='Duchenne muscular dystrophy', aliases=['DMD']),
        }

    def resolve_company(self, mention: str) -> CompanyMaster | None:
        needle = self._norm(mention)
        for company in self.store.companies.values():
            if needle in {self._norm(company.name), self._norm(company.ticker)}:
                return company
            if needle in {self._norm(a) for a in company.aliases}:
                return company
        return None

    def resolve_asset(self, mention: str) -> AssetMaster | None:
        needle = self._norm(mention)
        for asset in self.store.assets.values():
            if needle == self._norm(asset.canonical_name) or needle in {self._norm(a) for a in asset.aliases}:
                return asset
        return None

    def resolve_indication(self, mention: str) -> IndicationMaster | None:
        needle = self._norm(mention)
        for ind in self.store.indications.values():
            if needle == self._norm(ind.name) or needle in {self._norm(a) for a in ind.aliases}:
                return ind
        return None

    def resolve(self, company_mention: str | None = None, asset_mention: str | None = None, indication_mention: str | None = None) -> EntityResolutionResult:
        company = self.resolve_company(company_mention) if company_mention else None
        asset = self.resolve_asset(asset_mention) if asset_mention else None
        indication = self.resolve_indication(indication_mention) if indication_mention else None
        confidence = 0.0 + (0.35 if company else 0) + (0.35 if asset else 0) + (0.3 if indication else 0)
        notes = []
        if not company and company_mention:
            notes.append(f'Unresolved company mention: {company_mention}')
        if not asset and asset_mention:
            notes.append(f'Unresolved asset mention: {asset_mention}')
        if not indication and indication_mention:
            notes.append(f'Unresolved indication mention: {indication_mention}')
        return EntityResolutionResult(company=company, asset=asset, indication=indication, match_confidence=confidence, notes=notes)
