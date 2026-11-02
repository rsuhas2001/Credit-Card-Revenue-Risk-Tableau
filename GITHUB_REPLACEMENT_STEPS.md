# Replace the old GitHub project with this Tableau version (Mac)

The goal is to replace old Power BI files **inside the same GitHub repository** without deleting Git history.

## Step 1: extract the ZIP

Double-click the ZIP in Downloads. It should create:

`~/Downloads/Credit-Card-Revenue-Risk-Tableau/`

Check that the extracted folder contains `README.md` and `data/`.

## Step 2: rename the existing repository on GitHub

Open `https://github.com/rsuhas2001/Credit-Card-Revenue-Risk-Dashboard`.
Select **Settings → General → Repository name**, change it to:

`Credit-Card-Revenue-Risk-Tableau`

Click **Rename**. Do not select **Delete this repository**.

## Step 3: clone the renamed repo

Open Terminal:

```bash
cd ~/Downloads
git clone https://github.com/rsuhas2001/Credit-Card-Revenue-Risk-Tableau.git Credit-Card-Tableau-GitHub
```

If you have already cloned into `Credit-Card-Tableau-GitHub`, use `git pull` there instead of cloning twice.

## Step 4: back up existing files

```bash
cp -R ~/Downloads/Credit-Card-Tableau-GitHub ~/Downloads/Credit-Card-Tableau-Backup
```

## Step 5: replace the checked-out repo contents

```bash
rsync -av --delete --exclude='.git' \
  ~/Downloads/Credit-Card-Revenue-Risk-Tableau/ \
  ~/Downloads/Credit-Card-Tableau-GitHub/
```

`--delete` removes old files **only from this local clone**. The excluded `.git` directory preserves your repository history. Ensure the two folder paths are correct before running.

## Step 6: review changes, then push

```bash
cd ~/Downloads/Credit-Card-Tableau-GitHub
git status --short
git add -A
git commit -m "Replace Power BI project with Tableau analytics portfolio"
git push origin HEAD
```

The commit deletes the old Power BI files from the latest repository tree; it does not erase old commits. If prompted, sign in to GitHub or use your configured credentials. **Never enter passwords or tokens into a chat.**

## Step 7: verify

Open `https://github.com/rsuhas2001/Credit-Card-Revenue-Risk-Tableau`.

You should see a new README, `data/`, `src/`, `sql/`, `reports/`, `docs/`, `tests/`, and **no working Tableau workbook yet**. The README openly says the dashboard is still being built. The generated preview is clearly identified as a design mockup.

Once a working workbook opens and publishes in Tableau Public, add a `tableau/` folder with the verified `.twbx`, add a Tableau Public link in the README, commit, and push.
