
git

git
:   리누스 토발스가 개발한 분산 버전 관리 시스템

## 명령어

 * Revert
 
        git checkout filename
    
 * Create a branch and Fetch a branch
 
        # create
        git branch -a or git branch -r
        git checkout -b new_branch
        git push origin new_branch
        # fetch
        git branch or git branch -a or git branch -r
        git checkout origin/new_branch
        git checkout -b new_branch origin/new_branch
        # commit 
        git push origin/new_branch
    
 * Stash
 
        git stash
        git pull
        git stash pop
        git stash list
    
    