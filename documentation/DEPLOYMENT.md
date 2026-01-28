# Deployment

Regulate was deployed to **Heroku** using a standard Django production setup with Gunicorn, WhiteNoise and environment variables. Below are the exact steps followed during deployment, along with explanations of *why* each step was necessary.

Return to [README.md](../README.md)

---

## 1. Create the Heroku App

---

## 2. Configure Heroku Environment Variables


---

## 3. Prepare Django for Production

### Install Gunicorn (production WSGI server)


### Add WhiteNoise for serving static files


### Add STATIC_ROOT


---

## 4. Create the Procfile


---

## 5. Update `ALLOWED_HOSTS`


---

## 6. Disable Django Debug Mode


---

## 7. Push Code to GitHub


---

## 8. Connect Heroku to GitHub


---

## 9. Enable an Eco Dyno


---

## 10. Remove Temporary Static Setting


---

## 11. Verify Deployment


---
---

Return to [README.md](../README.md)
