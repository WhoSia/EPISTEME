"""P70-T4: exact selection/format decomposition and sensitivity bounds.

All-call executable correctness is observed; latent correctness of malformed
responses is NEVER imputed. Completion intervals are sensitivity constructs.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class Arm:
    slots:int
    format_valid:int
    grounded_correct:int

    def validate(self):
        if not (self.slots>0 and 0<=self.grounded_correct<=self.format_valid<=self.slots):
            raise ValueError("P70_SELECTION_INVALID_ARM")

    def f(self):
        self.validate()
        return F(self.format_valid,self.slots)

    def q(self):
        self.validate()
        if not self.format_valid:
            raise ValueError("P70_CONDITIONAL_UNDEFINED_NO_FORMAT_VALID")
        return F(self.grounded_correct,self.format_valid)

    def executable(self):
        self.validate()
        return F(self.grounded_correct,self.slots)

    def completion_interval(self):
        """Counterfactual completion for missing-format rows ONLY.

        This is not a statement that invalid responses possess an observed
        or definable latent semantic ground truth.
        """
        self.validate()
        return (F(self.grounded_correct,self.slots),
                F(self.grounded_correct+self.slots-self.format_valid,self.slots))


def diagnostic(a:Arm,b:Arm):
    """Exactly decompose executable gap a-b via b's conditional success."""
    a.validate();b.validate()
    fmt_component=(a.f()-b.f())*b.q()
    conditional_component=a.f()*(a.q()-b.q())
    difference=a.executable()-b.executable()
    assert fmt_component+conditional_component==difference
    al,au=a.completion_interval()
    bl,bu=b.completion_interval()
    return {
        "executable_difference":str(difference),
        "format_component_reference_b":str(fmt_component),
        "conditional_component_reference_b":str(conditional_component),
        "completion_sensitivity_lower":str(al-bu),
        "completion_sensitivity_upper":str(au-bl),
        "f_a":str(a.f()),"q_a":str(a.q()),
        "f_b":str(b.f()),"q_b":str(b.q()),
        "noncausal_note":"Reference-order-dependent exact arithmetic, not an output-contract causal effect.",
        "completion_note":"Hypothetical unknown-format semantic completions only; no observed latent semantic values.",
    }


# Frozen observed P69 pilot #37925719478, 48 slots per arm.
FROZEN={
    "gptoss120":{
        "strict_schema":Arm(48,48,36),
        "json_object":Arm(48,34,25),
    },
    "gemini":{
        "strict_schema":Arm(48,48,26),
        "json_object":Arm(48,47,23),
    },
}


def self_test():
    g=diagnostic(FROZEN["gptoss120"]["strict_schema"],FROZEN["gptoss120"]["json_object"])
    assert g["executable_difference"]=="11/48"
    assert g["format_component_reference_b"]==str(F(14,48)*F(25,34))
    assert g["conditional_component_reference_b"]==str(F(36,48)-F(25,34))
    assert g["completion_sensitivity_lower"]=="-1/16"
    assert g["completion_sensitivity_upper"]=="11/48"
    # Here diagnostic a=strict and b=json: completion difference
    # [36/48 - (25+14)/48, 36/48 - 25/48] = [-3/48,11/48].
    # The code must make that interval exactly, not impose a point estimate.
    print("P70_T4_GROQ_DERIVED",g)
    m=diagnostic(FROZEN["gemini"]["strict_schema"],FROZEN["gemini"]["json_object"])
    assert m["executable_difference"]=="1/16"
    assert m["completion_sensitivity_lower"]=="1/24"
    assert m["completion_sensitivity_upper"]=="1/16"
    assert sum([F(g["format_component_reference_b"]),F(g["conditional_component_reference_b"])])==F(11,48)
    for bad in (Arm(0,0,0),Arm(48,49,0),Arm(48,47,48)):
        try:bad.validate()
        except ValueError:pass
        else:raise AssertionError("P70_INVALID_SELECTION_ARM_ACCEPTED")
    print("P70_SELECTION_BOUNDS_SELFTEST_PASS observed_models=2 arithmetic_only=PASS provider_calls=0")


if __name__=="__main__":
    self_test()
