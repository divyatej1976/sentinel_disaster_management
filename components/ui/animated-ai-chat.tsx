import React, { useState } from 'react'
import { Loader2, Mic, Plus, SendHorizontal } from 'lucide-react'

interface AnimatedAIChatProps {
  onSendMessage: (message: string) => void;
  onUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  loading: boolean;
  uploading: boolean;
  placeholder: string;
}

export function AnimatedAIChat({ onSendMessage, onUpload, loading, uploading, placeholder }: AnimatedAIChatProps) {
  const [value, setValue] = useState('')
  const [listening, setListening] = useState(false)

  const submit = (event: React.FormEvent) => {
    event.preventDefault()
    const text = value.trim()
    if (!text || loading) return
    setValue('')
    onSendMessage(text)
  }

  const startVoice = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (!SpeechRecognition) {
      setListening(true)
      setTimeout(() => setListening(false), 900)
      return
    }
    const recognition = new SpeechRecognition()
    recognition.onstart = () => setListening(true)
    recognition.onresult = (event: any) => setValue(event.results[0][0].transcript)
    recognition.onend = () => setListening(false)
    recognition.start()
  }

  return (
    <form className="chat-composer" onSubmit={submit}>
      <label className="tool-icon" title="Upload notes (PDF, TXT, DOCX only)">
        {uploading ? <Loader2 className="spin" size={18} /> : <Plus size={20} />}
        <input type="file" multiple accept=".pdf,.txt,.docx" onChange={onUpload} disabled={uploading} className="hidden" />
      </label>
      <div className="composer-divider" />
      <input
        value={value}
        onChange={(event) => setValue(event.target.value)}
        placeholder={uploading ? "ATLAS is reading documents, please wait..." : placeholder}
        disabled={loading || uploading}
        className="flex-1 bg-transparent border-none outline-none text-sm text-foreground placeholder:text-muted-foreground"
      />
      <button type="button" className={`tool-icon ${listening ? 'hot' : ''}`} onClick={startVoice} disabled={loading || uploading}>
        <Mic size={18} />
      </button>

      <button type="submit" className="send-button" disabled={loading || uploading || !value.trim()}>
        {loading ? <Loader2 className="spin" size={18} /> : <SendHorizontal size={18} />}
      </button>
    </form>
  )
}
