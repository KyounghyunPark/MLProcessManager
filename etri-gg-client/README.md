## Getting Started

Install required libraries
```bash
pnpm install
```

run the development server:
```bash
pnpm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Deploy
Go to ".env.docker", change the value of NEXT_PUBLIC_AI_SERVER to your ip
```dotenv
NEXT_PUBLIC_AI_SERVER=YOUR_IP
```

Update the sub module
```bash
git submodule update --init
```

Build docker image
```bash
docker compose build
```

Start the production server
```bash
docker compose up -d
```

From the web browser, access the website at the url [http://YOUR_IP:8380](http://localhost:8380)