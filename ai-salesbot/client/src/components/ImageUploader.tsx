import { Button, FormItem, Input } from '@vkontakte/vkui'
import { useRef, useState } from 'react'
import api from '../app/api'

export default function ImageUploader({ botId, onUploaded }: { botId: number; onUploaded: (url: string, filename: string) => void }) {
  const inputRef = useRef<HTMLInputElement | null>(null)
  const [loading, setLoading] = useState(false)

  const onClick = () => inputRef.current?.click()

  const onChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    const form = new FormData()
    form.append('bot_id', String(botId))
    form.append('file', file)
    setLoading(true)
    try {
      const { data } = await api.post('/v1/uploads/image', form, { headers: { 'Content-Type': 'multipart/form-data' } })
      onUploaded(data.url, data.filename)
    } finally {
      setLoading(false)
    }
  }

  return (
    <FormItem top="Фото">
      <input ref={inputRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={onChange} />
      <Button loading={loading} onClick={onClick} size="m">
        Загрузить фото
      </Button>
    </FormItem>
  )
}