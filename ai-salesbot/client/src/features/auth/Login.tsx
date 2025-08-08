import bridge from '@vkontakte/vk-bridge'
import { Button, Div, Group, Panel, PanelHeader, Placeholder } from '@vkontakte/vkui'
import { useState } from 'react'
import { loginWithVkUserId } from '../../app/auth'

export default function Login() {
  const [vkUserId, setVkUserId] = useState<string | null>(null)
  const [status, setStatus] = useState<string>('')

  const getUser = async () => {
    const res = await bridge.send('VKWebAppGetUserInfo')
    setVkUserId(String(res.id))
  }

  const login = async () => {
    if (!vkUserId) return
    setStatus('Вход...')
    await loginWithVkUserId(vkUserId)
    setStatus('Успешно. Перейдите к списку ботов')
  }

  return (
    <Panel id="login">
      <PanelHeader>Вход</PanelHeader>
      <Group>
        <Div>
          <Placeholder header="MVP вход по VK user_id">
            <Button size="l" onClick={getUser} style={{ marginRight: 8 }}>
              Получить VK user_id
            </Button>
            <Button size="l" onClick={login} disabled={!vkUserId}>
              Войти
            </Button>
          </Placeholder>
          <div>{vkUserId ? `VK ID: ${vkUserId}` : ''}</div>
          <div>{status}</div>
        </Div>
      </Group>
    </Panel>
  )
}