<script>
    import fastapi from "../lib/api"
    import  {push} from 'svelte-spa-router'
    import Error from "../components/Error.svelte"
    import moment from 'moment/min/moment-with-locales'    

    moment.locale('ko')


     export let params = {}
//    const answer_id = params.answer_id

    let error = {detail:[]}
    let question_id = ""
    let content = "대한민국의 수도는 어디야?"
    let res_openapi = '';     

    let fruit = "NQ";
    

    function get_openapi(){
        let params = {
            type : fruit , 
            content :  content
        }
        fastapi('post', '/api/ai/openapi', params, (json) => {
            res_openapi = json.openapi
        }) 
    }


//    alert('answer_id' + answer_id)

    function update_answer(event){
        event.preventDefault()
        let url = "/api/answer/update"
        let params = {
            answer_id : answer_id,
            content : content,
        }

        fastapi('put',url,params, 
            (json)=>{
                push("/detail/"+question_id)
            },
            (json_error) => {
                error = json_error
            }            
        )
    }
</script>



<div class="container ">
    <h5 class="my-3 border-bottom pb-2">OPEN API</h5>
    <Error error={error} /> 
    <form method="post"  >
        <select bind:value={fruit} style="width:100px;">
            <option value="NQ">번역</option>
            <option value="VQ">영상분석(URL)</option>
            <option value="VQB">영상분석(BASE64)</option>
        </select>

        <div class="mb-3">
            <lable for="content">질문</lable>        
            <input type="text" class="form-control"  bind:value="{content}" />
            <button type="button" class="btn btn-primary" on:click={get_openapi} >  질문하기 </button>        
        </div>
        
        <div class="card-body">
            <input type="text"  class="form-control" bind:value={res_openapi}>
            <div class="card-text" style="white-space: pre-line;width:300px;">{res_openapi}</div>
        </div>
    </form>
    

</div>

