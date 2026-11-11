"""P77 W45 research cache identity selftest (synthetic, not production BIA run).

A documented BioImage Archive bia-converter source path tests destination
existence before conversion. This code demonstrates the additional source,
binary, argument, specification and output-proof keys needed to certify reuse.
"""
from dataclasses import dataclass
import hashlib

@dataclass(frozen=True)
class Request:
    source_sha256: str
    converter_sha256: str
    arguments: tuple[str, ...]
    ngff_spec: str

def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def identity(req: Request) -> str:
    return digest("\x1f".join([
        req.source_sha256, req.converter_sha256,
        "\x00".join(req.arguments), req.ngff_spec
    ]))

def source_like_exists_only(path_exists: bool) -> bool:
    return path_exists

def approved_reuse(path_exists: bool, req: Request, stored_key: str | None,
                   output_verified: bool) -> bool:
    return path_exists and stored_key == identity(req) and output_verified

def selftest() -> None:
    base = Request(digest("source_v1"), digest("converter_v1"),
                   ("--ngff-version=0.4",), "OME-NGFF-0.4")
    changes = [
        Request(digest("source_v2"), base.converter_sha256,
                base.arguments, base.ngff_spec),
        Request(base.source_sha256, digest("converter_v2"),
                base.arguments, base.ngff_spec),
        Request(base.source_sha256, base.converter_sha256,
                ("--ngff-version=0.5",), base.ngff_spec),
        Request(base.source_sha256, base.converter_sha256,
                base.arguments, "OME-NGFF-0.5"),
    ]
    assert len({identity(x) for x in [base, *changes]}) == 5
    for modified in changes:
        assert source_like_exists_only(True)
        assert not approved_reuse(True, modified, identity(base), True)
    assert approved_reuse(True, base, identity(base), True)
    assert not approved_reuse(True, base, identity(base), False)
    assert not approved_reuse(False, base, identity(base), True)
    print("PASS synthetic: 4 source/binary/args/spec changes blocked by sealed cache")
    print("PASS synthetic: valid unchanged output reused; invalid or absent rejected")
    print("LIMIT: did NOT run or inspect the production cache state")

if __name__ == "__main__":
    selftest()
