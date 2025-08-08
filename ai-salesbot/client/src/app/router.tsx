import { createBrowserRouter } from 'react-router-dom'
import Login from '../features/auth/Login'
import BotsList from '../features/bots/BotsList'
import BotEditor from '../features/bots/BotEditor'
import ChatSimulator from '../features/dialogs/ChatSimulator'
import Overview from '../features/analytics/Overview'
import Billing from '../features/billing/Billing'

const router = createBrowserRouter([
  { path: '/', element: <BotsList /> },
  { path: '/login', element: <Login /> },
  { path: '/bots/:id', element: <BotEditor /> },
  { path: '/dialogs/:id', element: <ChatSimulator /> },
  { path: '/analytics', element: <Overview /> },
  { path: '/billing', element: <Billing /> },
])

export default router