import { Button, Card, Div, Group, Panel, PanelHeader, SimpleCell, Spacing } from '@vkontakte/vkui'
import { useEffect, useState } from 'react'
import api from '../../app/api'
import { Link } from 'react-router-dom'

interface Bot {
  id: number
  owner_id: number
  name: string
  description: string
}

export default function BotsList() {
  const [bots, setBots] = useState<Bot[]>([])

  const fetchBots = async () => {
    const { data } = await api.get('/v1/bots')
    setBots(data)
  }

  useEffect(() => {
    fetchBots()
  }, [])

  const createBot = async () => {
    const { data } = await api.post('/v1/bots', {
      name: 'Новый товар',
      description: 'Описание',
      characteristics: {},
      images: [],
      price: 1000,
      discount_percent: 10,
      wholesale_price: 800,
      pay_url: '',
      pay_url_discount: '',
      bargaining_style: 'standard',
      faq: [],
      model_preset: '',
    })
    setBots((prev) => [data, ...prev])
  }

  return (
    <Panel id="bots">
      <PanelHeader>Мои боты</PanelHeader>
      <Group>
        <Div>
          <Button size="l" onClick={createBot}>
            Создать бота
          </Button>
        </Div>
        <Spacing size={16} />
        <Div>
          {bots.map((b) => (
            <Card key={b.id} style={{ marginBottom: 12, padding: 12 }}>
              <Link to={`/bots/${b.id}`}>{b.name}</Link>
              <div style={{ color: '#666' }}>{b.description}</div>
            </Card>
          ))}
        </Div>
      </Group>
    </Panel>
  )
}