# Todo Frontend - Phase II

Next.js 16+ frontend for the Todo application with TypeScript and Tailwind CSS.

## Technology Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Package Manager**: npm

## Setup

1. Copy environment file:
   ```bash
   cp .env.local.example .env.local
   ```

2. Configure `NEXT_PUBLIC_API_URL` to point to your backend.

3. Install dependencies:
   ```bash
   npm install
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Pages

| Route | Description |
|-------|-------------|
| / | Landing page |
| /login | User login |
| /register | User registration |
| /tasks | Task management (protected) |

## Components

- `AuthForm` - Login/register form with validation
- `TaskList` - List of tasks with loading/error states
- `TaskItem` - Individual task with toggle, edit, delete
- `TaskForm` - Modal form for creating/editing tasks

## Project Structure

```
frontend/
├── src/
│   ├── app/           # Next.js App Router pages
│   ├── components/    # React components
│   ├── lib/           # Utilities (api, auth)
│   └── types/         # TypeScript types
├── package.json
└── tailwind.config.ts
```

## Building for Production

```bash
npm run build
npm start
```
