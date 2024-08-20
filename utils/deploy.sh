python watch.py --no-watch
cd _build
git init .
git checkout -b 'gh-pages'
git add .
git commit -m 'auto build & deploy'
git remote add origin git@github.com-personal:CRiddler/wholesomehomecook.git
git push origin -u gh-pages --force
rm -rf ./.git
