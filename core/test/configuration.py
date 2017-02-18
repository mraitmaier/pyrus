
from pyrus.core.configuration import Configuration
from pyrus.core.testcase import TestCase
from pyrus.core.teststep import TestStep
from pyrus.core.action import ScriptedAction, NoOpAction

def runtests():
    # create some actions
    a0 = NoOpAction()
    a1 = ScriptedAction("scripts/test.py")
    a2 = ScriptedAction("scripts/test.rb")
    a3 = ScriptedAction("scripts/hello.jar")
    a4 = ScriptedAction("scripts/nonexistent.py")
    # steps
    s0 = TestStep("Empty step")
    s0.action = a0
    s1 = TestStep("PythonScript")
    s1.action = a1
    s2 = TestStep("RubyScript")
    s2.action = a3
    s3 = TestStep("Java JAR")
    s3.action = a3
    s4 = TestStep("Non-existent script")
    s4.action = a4
#    print("step0:" + str(s0))
#    print("step1:" + str(s1))
#    print("step2:" + str(s2))
#    print("step3:" + str(s3))
#    print("step4:" + str(s4))
    # cases
    tc0 = TestCase("Empty test case")
    tc0.addStep(s0)
    print("case0:" + str(tc0))
    tc1 = TestCase("The first case")
    tc1.addStep(s1)
    tc1.addStep(s2)
    print("case1:" + str(tc1))
    tc2 = TestCase("The Second Case")
    tc2.addStep(s3)
    tc2.addStep(s4)
    print("case2:" + str(tc2))

if __name__ == "__main__":
    runtests()
