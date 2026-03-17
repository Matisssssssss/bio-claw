from app.master_data.security_master import SecurityMaster


def test_security_master_resolves_aliases() -> None:
    master = SecurityMaster()
    master.load_demo_records()
    c = master.resolve_company('Neurocrine')
    assert c is not None
    assert c.ticker == 'NBIX'
    asset = master.resolve_asset('NBI-74788')
    assert asset is not None
    assert asset.canonical_name == 'crinecerfont'
