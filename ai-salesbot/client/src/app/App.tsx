import { AppRoot, AdaptivityProvider, ConfigProvider } from '@vkontakte/vkui'
import { RouterProvider } from 'react-router-dom'
import router from './router'
import '../styles/index.css'

export default function App() {
  return (
    <ConfigProvider>
      <AdaptivityProvider>
        <AppRoot>
          <RouterProvider router={router} />
        </AppRoot>
      </AdaptivityProvider>
    </ConfigProvider>
  )
}