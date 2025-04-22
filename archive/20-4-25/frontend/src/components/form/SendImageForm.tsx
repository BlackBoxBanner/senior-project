"use client"

import { sendImageAction } from "@/actions/sentImage";
import { FormEvent } from "react";
import { useFormStatus } from "react-dom";
import { Color603010, useColorRuleResult } from "@/provider/ColorRuleResult";

const SendImageForm = () => {
  const { setColorResult } = useColorRuleResult()

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const formData = new FormData(e.currentTarget);
      const result = await sendImageAction<Color603010>(formData);

      setColorResult((prev) => {
        return {
          ...prev,
          603010: result
        }
      })

    } catch (error) {
      console.error("Error submitting the image:", error);
    }
  }

  return (
    <div>
      <h2>60-30-10 color test</h2>
      <form onSubmit={handleSubmit}>
        <input name="image" type="file" accept="image/*" />
        <SubmitButton />
      </form>
    </div>
  )
}

const SubmitButton = () => {
  const { pending } = useFormStatus()

  return (
    <button disabled={pending} type="submit">Submit</button>
  )
}

export default SendImageForm;