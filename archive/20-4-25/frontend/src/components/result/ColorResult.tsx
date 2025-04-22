"use client"

import { useColorRuleResult } from "@/provider/ColorRuleResult";
import { cn } from "@/utils/cn";

const ColorResult = () => {
  const { colorResult } = useColorRuleResult();

  if (!colorResult || !colorResult[603010]) {
    return <h2 className="text-2xl font-bold">60-30-10 color test</h2>;
  }

  const {
    primary_color: primaryColor,
    secondary_color: secondaryColor,
    accent_color: accentColor,
    details,
  } = colorResult[603010];

  return (
    <div className="grid grid-cols-2 gap-2">
      <div>
        <h3 className="text-xl font-semibold">Primary color</h3>
        <div className="ml-4">
          <div className="flex items-center gap-2">
            <div>Color: {primaryColor.color.join(",")}</div>
            <div style={{ backgroundColor: `rgb(${primaryColor.color.join(",")})`, width: '20px', height: '20px', display: 'inline-block', marginLeft: '10px' }}></div>
          </div>
          <div>Percentage: {`${primaryColor.percentage.toFixed(2)}%`}</div>
        </div>
      </div>
      <div>
        <h3 className="text-xl font-semibold">Secondary color</h3>
        <div className="ml-4">
          <div className="flex items-center gap-2">
            <div>Color: {secondaryColor.color.join(",")}</div>
            <div style={{ backgroundColor: `rgb(${secondaryColor.color.join(",")})`, width: '20px', height: '20px', display: 'inline-block', marginLeft: '10px' }}></div>
          </div>
          <div>Percentage: {`${secondaryColor.percentage.toFixed(2)}%`}</div>
        </div>
      </div>
      <div>
        <h3 className="text-xl font-semibold">Accent color</h3>
        <div className="ml-4">
          <div className="flex items-center gap-2">
            <div>Color: {accentColor.color.join(",")}</div>
            <div style={{ backgroundColor: `rgb(${accentColor.color.join(",")})`, width: '20px', height: '20px', display: 'inline-block', marginLeft: '10px' }}></div>
          </div>
          <div>Percentage: {`${accentColor.percentage.toFixed(2)}%`}</div>
        </div>
      </div>
      <div>
        <h3 className="text-xl font-semibold">Rule followed: {colorResult[603010].rule_followed ? "Yes" : "No"}</h3>
        <div className="ml-4">
          <h4 className="text-lg font-medium">Details</h4>
          <div>Primary color: {details.primary_ok ? "Yes" : "No"}</div>
          <div>Secondary color: {details.secondary_ok ? "Yes" : "No"}</div>
          <div>Accent color: {details.accent_ok ? "Yes" : "No"}</div>
        </div>
      </div>
      <div className="w-full col-span-2">
        {/* display all 3 colors in a percentage. */}
        <h3 className="text-xl font-semibold">Color percentages</h3>
        <div className="flex">
          <div style={{ backgroundColor: `rgb(${primaryColor.color.join(",")})`, width: `${primaryColor.percentage.toFixed(2)}%`, height: '20px', display: 'inline-block' }}></div>
          <div style={{ backgroundColor: `rgb(${secondaryColor.color.join(",")})`, width: `${secondaryColor.percentage.toFixed(2)}%`, height: '20px', display: 'inline-block' }}></div>
          <div style={{ backgroundColor: `rgb(${accentColor.color.join(",")})`, width: `${accentColor.percentage.toFixed(2)}%`, height: '20px', display: 'inline-block' }}></div>
        </div>
      </div>
    </div>
  );
}

export default ColorResult;