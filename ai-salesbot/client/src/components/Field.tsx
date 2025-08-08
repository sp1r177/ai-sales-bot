import { FormItem } from '@vkontakte/vkui'
import { ReactNode } from 'react'

export default function Field({ label, children }: { label: string; children: ReactNode }) {
  return <FormItem top={label}>{children}</FormItem>
}