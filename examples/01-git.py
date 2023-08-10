from linguine.git import Git

proj = Git(".")
print(proj._repo.status())