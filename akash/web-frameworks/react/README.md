# React


Deploy your React applications on the decentralized Blazing Core Network. This template provides a basic setup for serving a production-ready React app using Nginx.

## Prerequisites

- A built React application (run `npm run build` in your React project to generate the `build` folder)

## Deployment Steps

1. **Build your React app:**
   ```bash
   npm run build
   ```

2. **Prepare your deployment:**
   - This template uses Nginx to serve static files.
   - Upload your `build` folder contents to the persistent storage at `/usr/share/nginx/html` during deployment.

   - Access your React app at the exposed endpoint (port 80).

## Configuration

- **Port:** 80
- **Web Server:** Nginx (Alpine)
- **Storage:** 128Mi (expand as needed for your app)

## Customization

- To include your build files directly, create a custom Docker image based on `nginx:alpine` and copy your build files to `/usr/share/nginx/html`.

## Resources

- [React Official Documentation](https://react.dev/)
