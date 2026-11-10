export const copyToClipboard = async (text: string) =>
  navigator.clipboard?.writeText(text)
