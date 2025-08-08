import { Button, Group, Panel, PanelHeader, Radio } from '@vkontakte/vkui'
import { useState } from 'react'
import api from '../../app/api'

export default function Billing() {
  const [plan, setPlan] = useState('free')
  const subscribe = async () => {
    await api.post('/v1/billing/subscribe', null, { params: { plan } })
    alert(`Подключен план: ${plan}`)
  }
  return (
    <Panel id="billing">
      <PanelHeader>Тарифы</PanelHeader>
      <Group>
        <Radio name="plan" value="free" checked={plan === 'free'} onChange={() => setPlan('free')}>
          Free: 1 бот, 5 диалогов/мес
        </Radio>
        <Radio name="plan" value="start" checked={plan === 'start'} onChange={() => setPlan('start')}>
          Start: 1 бот, 300 диалогов — 1990₽
        </Radio>
        <Radio name="plan" value="pro" checked={plan === 'pro'} onChange={() => setPlan('pro')}>
          Pro: 3 бота, 1000 диалогов — 4990₽
        </Radio>
        <Radio name="plan" value="premium" checked={plan === 'premium'} onChange={() => setPlan('premium')}>
          Premium: 5 ботов, 3000 диалогов — 9990₽
        </Radio>
        <Button onClick={subscribe}>Подключить</Button>
      </Group>
    </Panel>
  )
}