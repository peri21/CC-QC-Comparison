from qiskit_ibm_runtime import QiskitRuntimeService

# Ver las cuentas guardadas
saved_accounts = QiskitRuntimeService.saved_accounts()
print(saved_accounts)
