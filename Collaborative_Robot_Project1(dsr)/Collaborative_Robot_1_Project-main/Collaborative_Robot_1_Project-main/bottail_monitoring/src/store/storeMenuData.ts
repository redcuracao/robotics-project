import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { MenuDataType, MenuItemType } from '@/types/menuDataType'

const useMenuStore = defineStore('menu', () => {
  // 메뉴 정보
  const menuList: MenuDataType[] = [
    {
      category: 'whisky',
      name: '위스키 베이스',
      item: [
        {
          category: 'manhattan',
          name: '맨해튼',
          price: 1000,
          description: '위스키와 베르무트의 조화가 돋보이는 클래식 칵테일',
          image: '/images/manhattan.webp',
        },
        {
          category: 'jackCoke',
          name: '잭콕',
          price: 900,
          description: '잭다니엘과 콜라의 부담 없는 하이볼 스타일',
          image: '/images/jackcoke.webp',
        },
        {
          category: 'godfather',
          name: '갓파더',
          price: 1000,
          description: '위스키에 아마레또를 더한 달콤하고 묵직한 맛',
          image: '/images/godfather.webp',
        },
        {
          category: 'oldFashioned',
          name: '올드 패션드',
          price: 1100,
          description: '설탕과 비터로 위스키 본연의 풍미를 살린 정통 칵테일',
          image: '/images/old_fashioned.webp',
        },
        {
          category: 'highball',
          name: '하이볼',
          price: 800,
          description: '탄산과 위스키의 청량하고 가벼운 조합',
          image: '/images/highball.webp',
        },
      ],
    },
    {
      category: 'jin',
      name: '진 베이스',
      item: [
        {
          category: 'martini',
          name: '마티니',
          price: 1100,
          description: '진과 드라이 베르무트의 깔끔한 어른의 맛',
          image: '/images/martini.webp',
        },
        {
          category: 'ginTonic',
          name: '진토닉',
          price: 900,
          description: '허브 향의 진과 토닉워터의 상쾌한 조합',
          image: '/images/gin_tonic.webp',
        },
        {
          category: 'longIslandIcedTea',
          name: '롱 아일랜드 아이스 티',
          price: 1000,
          description: '여러 술이 어우러진 강렬하지만 의외로 부드러운 칵테일',
          image: '/images/long_island.webp',
        },
      ],
    },
    {
      category: 'vodka',
      name: '보드카 베이스',
      item: [
        {
          category: 'moscowMule',
          name: '모스코 뮬',
          price: 800,
          description: '보드카와 진저비어의 상쾌한 스파이시함',
          image: '/images/moscow_mule.webp',
        },
        {
          category: 'blackRussaian',
          name: '블랙 러시안',
          price: 900,
          description: '보드카와 커피 리큐르의 달콤 쌉싸름한 조합',
          image: '/images/black_russain.webp',
        },
        {
          category: 'cosmopolitan',
          name: '코스모폴리탄',
          price: 1100,
          description: '상큼한 크랜베리와 라임이 어우러진 세련된 맛',
          image: '/images/cosmopolitan.webp',
        },
        {
          category: 'buleLagoon',
          name: '블루 라군',
          price: 1000,
          description: '선명한 블루 컬러의 달콤하고 청량한 칵테일',
          image: '/images/blue_lagoon.webp',
        },
        {
          category: 'seaBreeze',
          name: '시 브리즈',
          price: 1100,
          description: '과일 주스가 어우러진 가볍고 산뜻한 맛',
          image: '/images/sea_breeze.webp',
        },
      ],
    },
    {
      category: 'rum',
      name: '럼 베이스',
      item: [
        {
          category: 'mojito',
          name: '모히또',
          price: 1100,
          description: '민트와 라임이 어우러진 대표적인 상큼 칵테일',
          image: '/images/mojito.webp',
        },
        {
          category: 'bacardi',
          name: '바카디',
          price: 1000,
          description: '럼의 깔끔한 풍미를 느낄 수 있는 베이직 칵테일',
          image: '/images/bacardi.webp',
        },
        {
          category: 'cubalibre',
          name: '쿠바 리브레',
          price: 900,
          description: '럼과 콜라에 라임을 더한 시원한 맛',
          image: '/images/cuba_libre.webp',
        },
      ],
    },
    {
      category: 'liqueur',
      name: '리큐르 베이스',
      item: [
        {
          category: 'midoriSour',
          name: '미도리 사워',
          price: 1100,
          description: '멜론 리큐르의 달콤하고 상큼한 맛',
          image: '/images/midori.webp',
        },
        {
          category: 'juneBug',
          name: '준벅',
          price: 900,
          description: '열대과일 풍미의 달콤한 파티 칵테일',
          image: '/images/june_bug.webp',
        },
        {
          category: 'greenWidow',
          name: '그린 위도우',
          price: 1000,
          description: '허브 향이 인상적인 독특한 리큐르 칵테일',
          image: '/images/green_widow.webp',
        },
        {
          category: 'fuzzyNavel',
          name: '퍼지 네이블',
          price: 1000,
          description: '복숭아 향이 부드럽게 퍼지는 달콤한 칵테일',
          image: '/images/fuzzy_navel.webp',
        },
        {
          category: 'spritz',
          name: '스프릿츠',
          price: 1100,
          description: '가볍고 탄산감 있는 이탈리아식 아페리티프',
          image: '/images/spritz.webp',
        },
        {
          category: 'brainHemorrhage',
          name: '브레인 헤머리지',
          price: 1200,
          description: '비주얼이 강렬한 달콤한 샷 칵테일',
          image: '/images/brain_hemorrhage.webp',
        },
      ],
    },
  ]

  // 메뉴판 버튼 클릭 상태
  const menuState = ref('whisky')
  const setMenuState = (category: string) => {
    menuState.value = category
  }

  // 어드민 페이지 버튼 클릭 상태
  const adminMenuState = ref('orderDetails')
  const setAdminMenuState = (category: string) => {
    adminMenuState.value = category
  }

  // 주문하려는 아이템 정보
  const orderItemInfo = ref({} as MenuItemType)
  const setOrderItemInfo = (data: MenuItemType) => {
    orderItemInfo.value = data
  }

  return {
    menuList,
    menuState,
    setMenuState,
    orderItemInfo,
    setOrderItemInfo,
    adminMenuState,
    setAdminMenuState,
  }
})

export default useMenuStore
