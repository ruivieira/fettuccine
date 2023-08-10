from fettuccine.git import Git

proj = Git(".")
print(proj._repo.status())

print(f"Branch main exists? {proj.branches.branch_exists('main')}")

proj.branches.create_branch("test-0.3.2")

b = proj.branches.create_minor_branch("test-$version")
print(b)
print(type(b))
b = proj.branches.create_major_branch("test-$version")
print(b)
b = proj.branches.create_patch_branch("test-$version")
print(b)
