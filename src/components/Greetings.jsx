export default defineComponent((props) => {
  const count = ref(0)

  return () => (
    <h1 class='m-0 bg-green-600 text-white text-center py-[8px]'>
      <span>Hello {props.name}! Counting {count.value}</span>
      <button class='ml-3 bg-gray-500/30 border border-gray-600/30 rounded-md w-7' onClick={() => count.value++}>+</button>
      <button class='ml-3 bg-gray-500/30 border border-gray-600/30 rounded-md w-7' onClick={() => count.value--}>-</button>
    </h1>
  )
}, {
  name: 'Greetings',
  props: ['name'],
})
