import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../../app/api'
import {
  Button,
  Div,
  FormItem,
  Group,
  Input,
  Panel,
  PanelHeader,
  Radio,
  Textarea,
} from '@vkontakte/vkui'
import ImageUploader from '../../components/ImageUploader'

export default function BotEditor() {
  const { id } = useParams()
  const [bot, setBot] = useState<any | null>(null)

  const fetchBot = async () => {
    const { data } = await api.get(`/v1/bots/${id}`)
    setBot(data)
  }

  useEffect(() => {
    fetchBot()
  }, [id])

  const save = async () => {
    await api.put(`/v1/bots/${id}`, bot)
    await fetchBot()
  }

  if (!bot) return null

  return (
    <Panel id="bot-editor">
      <PanelHeader>Редактор бота</PanelHeader>
      <Group>
        <Div>
          <FormItem top="Название">
            <Input value={bot.name} onChange={(e) => setBot({ ...bot, name: e.target.value })} />
          </FormItem>
          <FormItem top="Описание">
            <Textarea value={bot.description} onChange={(e) => setBot({ ...bot, description: e.target.value })} />
          </FormItem>
          <FormItem top="Характеристики (JSON)">
            <Textarea
              value={JSON.stringify(bot.characteristics || {}, null, 2)}
              onChange={(e) => {
                try {
                  const val = JSON.parse(e.target.value)
                  setBot({ ...bot, characteristics: val })
                } catch {}
              }}
            />
          </FormItem>
          <FormItem top="Цена">
            <Input type="number" value={bot.price} onChange={(e) => setBot({ ...bot, price: Number(e.target.value) })} />
          </FormItem>
          <FormItem top="Скидка, % (макс)">
            <Input
              type="number"
              value={bot.discount_percent}
              onChange={(e) => setBot({ ...bot, discount_percent: Number(e.target.value) })}
            />
          </FormItem>
          <FormItem top="Оптовая цена">
            <Input
              type="number"
              value={bot.wholesale_price}
              onChange={(e) => setBot({ ...bot, wholesale_price: Number(e.target.value) })}
            />
          </FormItem>
          <FormItem top="Ссылка на оплату">
            <Input value={bot.pay_url || ''} onChange={(e) => setBot({ ...bot, pay_url: e.target.value })} />
          </FormItem>
          <FormItem top="Ссылка на оплату (со скидкой)">
            <Input
              value={bot.pay_url_discount || ''}
              onChange={(e) => setBot({ ...bot, pay_url_discount: e.target.value })}
            />
          </FormItem>
          <FormItem top="Стиль торга">
            <Radio
              name="style"
              value="soft"
              checked={bot.bargaining_style === 'soft'}
              onChange={() => setBot({ ...bot, bargaining_style: 'soft' })}
            >
              soft
            </Radio>
            <Radio
              name="style"
              value="standard"
              checked={bot.bargaining_style === 'standard'}
              onChange={() => setBot({ ...bot, bargaining_style: 'standard' })}
            >
              standard
            </Radio>
            <Radio
              name="style"
              value="hard"
              checked={bot.bargaining_style === 'hard'}
              onChange={() => setBot({ ...bot, bargaining_style: 'hard' })}
            >
              hard
            </Radio>
          </FormItem>
          <FormItem top="FAQ (по одному на строку)">
            <Textarea
              value={(bot.faq || []).join('\n')}
              onChange={(e) => setBot({ ...bot, faq: e.target.value.split('\n').filter(Boolean) })}
            />
          </FormItem>
          <ImageUploader
            botId={Number(id)}
            onUploaded={(url, filename) => setBot({ ...bot, images: [...(bot.images || []), filename] })}
          />
          <Button size="l" onClick={save}>
            Сохранить
          </Button>
        </Div>
      </Group>
    </Panel>
  )
}