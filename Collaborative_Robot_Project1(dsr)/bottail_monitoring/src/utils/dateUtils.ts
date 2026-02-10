/* eslint-disable @typescript-eslint/no-explicit-any */
export const getNowDate = () => {
  const today = new Date()

  const year = today.getFullYear()
  const month = ('0' + (today.getMonth() + 1)).slice(-2)
  const day = ('0' + today.getDate()).slice(-2)

  const hour = ('0' + today.getHours()).slice(-2)
  const minutes = ('0' + today.getMinutes()).slice(-2)
  const seconds = ('0' + today.getSeconds()).slice(-2)

  return `${year}-${month}-${day} ${hour}:${minutes}:${seconds}`
}

// delay 마다 한번씩 요청
export const throttle = <T extends (...args: any[]) => void>(fn: T, delay: number): T => {
  let last = 0
  return function (...args: any[]) {
    const now = Date.now()
    if (now - last >= delay) {
      last = now
      fn(...args)
    }
  } as T
}

export const formatTimestamp = (timestamp: number): string => {
  return new Date(timestamp).toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}
