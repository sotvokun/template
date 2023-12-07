import { defineComponent } from "vue";

export default defineComponent((props) => {
  return () => (
    <h1 class='m-0 bg-green-6 text-white text-center'>
      Hello {props.name}!
    </h1>
  )
}, {
  name: 'Greetings',
  props: ['name'],
})
