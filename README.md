# Portfolio Site — starter

A simple, clean, Apple-inspired one-page portfolio. Everything is plain HTML/CSS/JS — no build step, no dependencies.

## Files
- `index.html` — content and structure
- `styles.css` — all styling (colors/fonts are CSS variables at the top — easy to restyle)
- `script.js` — scroll animations, nav background, work filters
- `CNAME` — tells GitHub Pages which custom domain to use

## Editing in VS Code
Just open the folder and edit. Open `index.html` with a Live Server extension (or double-click it) to preview locally in your browser as you go.

To change colors/fonts, edit the `:root` block at the top of `styles.css`.

## Pushing to GitHub
1. Create a new repo on GitHub (e.g. `portfolio`)
2. In this folder:
   ```
   git init
   git add .
   git commit -m "Initial portfolio"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
   git push -u origin main
   ```
3. In the repo → **Settings → Pages** → set source to the `main` branch, root folder
4. Wait a minute, GitHub will give you a `yourusername.github.io/repo-name` URL to confirm it's live

## Linking your Fasthosts domain
1. Open `CNAME` in this project and replace `yourdomain.com` with your actual domain (e.g. `janedoe.com`), commit and push
2. In GitHub → repo → **Settings → Pages → Custom domain**, enter the same domain and save
3. In Fasthosts:
   - Log in → **Domain Names** → select your domain → **Configure Advanced DNS**
   - Add an **A record** with a blank/root host name, pointing to each of these IPs (add all four):
     ```
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
     ```
   - Add a **CNAME record** with host name `www` pointing to `YOUR-USERNAME.github.io`
   - Save
4. Wait for DNS to propagate (usually under an hour, can take up to 48)
5. Back in GitHub Pages settings, tick **Enforce HTTPS** once it becomes available

## What to customize first
- Your name, title, and tagline in the hero (`index.html`)
- The four placeholder project cards — swap in real project names, descriptions, and images (replace `.card__media` divs with `<img>` tags)
- About paragraph
- Email and social links in the contact section
