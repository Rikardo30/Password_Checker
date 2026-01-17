from Vault_Master import add_entry, load_entries

mp = input("Master password: ")

add_entry(mp, "gmail", "cardo@gmail.com", "SuperSecret123!")
print(load_entries(mp))