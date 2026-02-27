import PhysLean

/-!
# IQT — Hello World

A basic smoke test to verify the Lean + PhysLean toolchain is working.
-/

/-- A trivial theorem to confirm Lean compiles. -/
theorem hello_iqt : 1 + 1 = 2 := by norm_num

#check hello_iqt
#eval IO.println "Hello from IQT!"
