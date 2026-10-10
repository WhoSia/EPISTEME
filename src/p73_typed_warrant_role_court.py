"""P73 P3: claim-scoped typed proof provenance preservation, finite toy only.

A rename of handles can preserve the warrant while exact byte equality fails.
Unchanged final decision can mask invalidated source authority. A bijection is
a sufficient source-preserving witness only under externally justified roles.
"""
from __future__ import annotations
from dataclasses import dataclass
import json

@dataclass(frozen=True)
class Premise:
    handle: str
    source: str
    role: str
    time_scope: str
    authority: bool

@dataclass(frozen=True)
class Proof:
    claim: str
    premises: tuple[Premise,...]
    required_handles: tuple[str,...]

def proof_valid(p:Proof):
    d={x.handle:x for x in p.premises}
    return (len(d)==len(p.premises) and
       all(h in d and d[h].authority for h in p.required_handles))

def certify_transport(before:Proof,after:Proof,phi:dict[str,str], *,
                      external_provenance_verified:bool=False):
    if not external_provenance_verified:
        return "HOLD_EXTERNAL_AUTHORITY"
    old={x.handle:x for x in before.premises}
    new={x.handle:x for x in after.premises}
    if before.claim!=after.claim or set(phi)!=set(old) or len(set(phi.values()))!=len(phi):
        return "HOLD_NONBIJECTIVE_OR_CLAIM_MISMATCH"
    if set(phi.values())!=set(new):
        return "HOLD_TARGET_SUPPORT_MISMATCH"
    if not proof_valid(before) or not proof_valid(after):
        return "HOLD_INVALID_PREMISE"
    if tuple(phi[x] for x in before.required_handles)!=after.required_handles:
        return "HOLD_PROOF_DEPENDENCY_MISMATCH"
    for handle,atom in old.items():
        target=new[phi[handle]]
        if (atom.source,atom.role,atom.time_scope,atom.authority)!=(
            target.source,target.role,target.time_scope,target.authority):
            return "HOLD_PROVENANCE_SCOPE_OR_ROLE_CHANGE"
    return "CONDITIONAL_TYPED_WARRANT_TRANSPORT_PASS"

def test():
    base=Proof("MIGRATE",(Premise("x","sourceA","supports","t0",True),),("x",))
    renamed=Proof("MIGRATE",(Premise("alpha","sourceA","supports","t0",True),),("alpha",))
    assert proof_valid(base) and proof_valid(renamed)
    assert base!=renamed
    assert certify_transport(base,renamed,{"x":"alpha"})=="HOLD_EXTERNAL_AUTHORITY"
    assert certify_transport(base,renamed,{"x":"alpha"},external_provenance_verified=True)=="CONDITIONAL_TYPED_WARRANT_TRANSPORT_PASS"
    # Retaining decision 'MIGRATE' does not preserve the authority of this
    # warrant: the substitute may be supported by another different source.
    alternative=Proof("MIGRATE",(Premise("beta","sourceB","supports","t0",True),),("beta",))
    assert proof_valid(alternative)
    assert certify_transport(base,alternative,{"x":"beta"},external_provenance_verified=True)=="HOLD_PROVENANCE_SCOPE_OR_ROLE_CHANGE"
    time_change=Proof("MIGRATE",(Premise("alpha","sourceA","supports","t1",True),),("alpha",))
    assert certify_transport(base,time_change,{"x":"alpha"},external_provenance_verified=True)=="HOLD_PROVENANCE_SCOPE_OR_ROLE_CHANGE"
    revoked=Proof("MIGRATE",(Premise("alpha","sourceA","supports","t0",False),),("alpha",))
    assert certify_transport(base,revoked,{"x":"alpha"},external_provenance_verified=True)=="HOLD_INVALID_PREMISE"
    assert certify_transport(base,renamed,{"x":"alpha","other":"alpha"},external_provenance_verified=True)=="HOLD_NONBIJECTIVE_OR_CLAIM_MISMATCH"
    return {"kind":"P73_P3_TYPED_PROOF_ROLE_RENAMING_COURT",
       "renaming_can_preserve_proof":"CONDITIONAL_PASS",
       "same_decision_different_provenance":"NO_CONTINUITY_CERTIFICATE",
       "time_shift_or_revocation":"HOLD",
       "real_independent_provenance_witnesses":0,
       "claims_of_new_theorem":"NONE",
       "actual_human_judgments":0,"model_calls":0}

if __name__=="__main__":
    r=test()
    print("P73_P3_TYPED_WARRANT_ROLE_TEST_PASS renaming_sufficient_only=true calls=0")
    print(json.dumps(r,indent=2,sort_keys=True))
