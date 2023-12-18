export default function Greetings(props: { name: string }) {
  return (
    <h1 className='m-0 bg-green-6 text-white text-center'>
      Hello {props.name}!
    </h1>
  )
}
