"use client"
import { createContext, useContext, useState } from "react"

export type Color603010 = {
  primary_color: {
    color: Array<number>
    percentage: number
  }
  secondary_color: {
    color: Array<number>
    percentage: number
  }
  accent_color: {
    color: Array<number>
    percentage: number
  }
  rule_followed: boolean
  details: {
    primary_ok: boolean
    secondary_ok: boolean
    accent_ok: boolean
  }
}

type ColorRuleResult = {
  603010?: Color603010
}

const ColorRuleResultContext = createContext<{
  colorResult: ColorRuleResult | undefined
  setColorResult: React.Dispatch<React.SetStateAction<ColorRuleResult | undefined>>
}>({
  colorResult: undefined,
  setColorResult: () => { }
})

export const ColorRuleResultProvider = ({ children }: { children: Readonly<React.ReactNode> }) => {
  const [colorResult, setColorResult] = useState<ColorRuleResult>()
  return (
    <ColorRuleResultContext.Provider value={{ colorResult, setColorResult }}>
      {children}
    </ColorRuleResultContext.Provider>
  )
}

export const useColorRuleResult = () => {
  return useContext(ColorRuleResultContext)
}