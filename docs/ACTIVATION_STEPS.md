# Finish the GitHub profile and website settings

The application projects and website source files are already committed. These final actions require GitHub account/repository administration controls, which the connected editing interface does not provide.

## 1. Rename the portfolio repository

1. Open [the repository settings](https://github.com/Dhemiladhe201/hello/settings).
2. Under **General → Repository name**, change `hello` to `data-science-portfolio`.
3. Click **Rename**.

GitHub normally redirects standard repository links after a rename. GitHub Pages URLs do not follow the same redirect rule, so rename **before** enabling Pages.

## 2. Enable the website

1. In the renamed repository go to **Settings → Pages**.
2. Under **Build and deployment**, choose **GitHub Actions** as the source.
3. Open the **Actions** tab.
4. Select **Publish portfolio website (after Pages is enabled)** and choose **Run workflow**, on branch `main`.
5. Check that the deployment succeeded. Copy the actual published URL from the workflow's deployment environment. Do not assume it is live until verified.

The website source is `docs/index.html`, and the dashboard is at `docs/dashboard/index.html`. The live dashboard displays results generated from an explicitly synthetic retail dataset.

## 3. Display a GitHub profile introduction

1. Open [New repository](https://github.com/new).
2. Name the public repository **Dhemiladhe201** (exactly the account name).
3. Initialize it with a `README.md`.
4. Replace its README contents with the prepared [profile introduction](https://github.com/Dhemiladhe201/hello/blob/main/PROFILE_README.md) from the portfolio repository, keeping in mind that the links to `hello` will redirect after renaming. Save the changes.

GitHub displays the README from a *public repository named after the username* on the personal profile. Merely storing `PROFILE_README.md` inside the portfolio repository is not sufficient.

## 4. Power BI

The repository includes a detailed [Power BI Desktop build guide](https://github.com/Dhemiladhe201/hello/blob/main/projects/customer-analytics-sql/POWER_BI_BUILD.md) and reproducible generated data. It does **not** include a tested `.pbix` file. That requires Power BI Desktop and opening/saving a report there, which is separate from the GitHub repository editing actions available here.
