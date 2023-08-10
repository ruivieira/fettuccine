from linguine.git import Git

proj = Git(".")
print(proj._repo.status())

print(f"Branch main exists? {proj.branch_exists('main')}")

proj.create_branch("test-1")