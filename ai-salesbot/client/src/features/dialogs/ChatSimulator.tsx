import { Button, Div, Group, Input, Panel, PanelHeader } from '@vkontakte/vkui'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../../app/api'

export default function ChatSimulator() {
  const { id } = useParams()
  const [dialogId, setDialogId] = useState<number | null>(null)
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([])
  const [text, setText] = useState('')

  useEffect(() => {
    const start = async () => {
      const { data } = await api.post('/v1/dialogs/start', { bot_id: Number(id) })
      setDialogId(data.id)
    }
    start()
  }, [id])

  const send = async () => {
    if (!dialogId || !text.trim()) return
    await api.post(`/v1/dialogs/${dialogId}/message`, { text })
    const { data: all } = await api.get(`/v1/dialogs/${dialogId}`)
    setMessages(all)
    setText('')
  }

  return (
    <Panel id="chat">
      <PanelHeader>Чат</PanelHeader>
      <Group>
        <Div>
          <div style={{ minHeight: 200, border: '1px solid #eee', padding: 8 }}>
            {messages.map((m, i) => (
              <div key={i} style={{ marginBottom: 8 }}>
                <b>{m.sender}:</b> {m.text}
              </div>
            ))}
          </div>
        </Div>
        <Div style={{ display: 'flex', gap: 8 }}>
          <Input value={text} onChange={(e) => setText(e.target.value)} placeholder="Ваше сообщение" />
          <Button onClick={send}>Отправить</Button>
        </Div>
      </Group>
    </Panel>
  )
}