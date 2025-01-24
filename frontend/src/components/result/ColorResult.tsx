"use client"

import { useColorRuleResult } from "@/provider/ColorRuleResult";

const ColorResult = () => {
  const { colorResult } = useColorRuleResult();

  if (!colorResult || !colorResult[603010]) {
    return <h2 className="text-2xl font-bold">60-30-10 color test</h2>;
  }

  const primaryColor = colorResult[603010].primary_color;
  const secondaryColor = colorResult[603010].secondary_color;
  const accentColor = colorResult[603010].accent_color;
  const details = colorResult[603010].details;

  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="mb-4">
        <h3 className="text-xl font-semibold">Primary color</h3>
        <div className="ml-4">
          <div className="flex items-center gap-2">
            <div>Color: {primaryColor.color.join(",")}</div>
          </div>
          <div>Percentage: {`${primaryColor.percentage.toFixed(2)}%`}</div>
        </div>
      </div>
      <div className="mb-4">
        <h3 className="text-xl font-semibold">Secondary color</h3>
        <div className="ml-4">
          <div className="flex items-center gap-2">
            <div>Color: {secondaryColor.color.join(",")}</div>
          </div>
          <div>Percentage: {`${secondaryColor.percentage.toFixed(2)}%`}</div>
        </div>
      </div>
      <div className="mb-4">
        <h3 className="text-xl font-semibold">Accent color</h3>
        <div className="ml-4">
          <div className="flex items-center gap-2">
            <div>Color: {accentColor.color.join(",")}</div>
          </div>
          <div>Percentage: {`${accentColor.percentage.toFixed(2)}%`}</div>
        </div>
      </div>
      <div className="mb-4">
        <h3 className="text-xl font-semibold">Rule followed: {colorResult[603010].rule_followed ? "Yes" : "No"}</h3>
        <div className="ml-4">
          <h4 className="text-lg font-medium">Details</h4>
          <div>Primary color: {details.primary_ok ? "Yes" : "No"}</div>
          <div>Secondary color: {details.secondary_ok ? "Yes" : "No"}</div>
          <div>Accent color: {details.accent_ok ? "Yes" : "No"}</div>
        </div>
      </div>
    </div>
  );
}

export default ColorResult;