import { Group, Panel, PanelHeader, SimpleCell } from '@vkontakte/vkui'
import { useEffect, useState } from 'react'
import api from '../../app/api'

export default function Overview() {
  const [data, setData] = useState<any>({})
  useEffect(() => {
    api.get('/v1/analytics/overview').then((res) => setData(res.data))
  }, [])
  return (
    <Panel id="analytics">
      <PanelHeader>Аналитика</PanelHeader>
      <Group>
        <SimpleCell>Диалогов всего: {data.total_dialogs}</SimpleCell>
        <SimpleCell>Оплаченных: {data.paid_dialogs}</SimpleCell>
        <SimpleCell>Конверсия: {data.conversion_percent}%</SimpleCell>
        <SimpleCell>Средняя скидка: {data.avg_discount_percent}%</SimpleCell>
      </Group>
    </Panel>
  )
}