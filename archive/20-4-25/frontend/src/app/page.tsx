import SendImageForm from "@/components/form/SendImageForm";
import ColorResult from "@/components/result/ColorResult";

export default function Home() {
  return (
    <div className="grid grid-cols-2 gap-4 p-4">
      <SendImageForm />
      <ColorResult />
      <div>ColorResult1</div>
      <div>ColorResult2</div>
    </div>
  );
}
