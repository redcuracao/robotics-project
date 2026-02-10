export type MenuDataType = {
  category: string
  name: string
  item: MenuItemType[]
}

export type MenuItemType = {
  category: string
  name: string
  price: number
  description: string
  image: string
}

export type AdminMenuType = {
  title: string
  category: string
}

export type OrderDetailsType = {
  category: string
  name: string
  price: number
  time: string
}
