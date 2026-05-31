<script>
    import fastapi from "../lib/api"
    import {link} from 'svelte-spa-router'
    import {page, keyword, is_login} from "../lib/store"
    import moment from 'moment/min/moment-with-locales'

    moment.locale('ko')

    let size = 10
    let total = 0
    let kw = ''
    $: total_page = Math.ceil(total/size)


    let question_list = []

    

    function get_question_list(){
        let params = {
            page : $page,
            size : size,
            keyword:$keyword, 
        }
        fastapi('get', '/api/question/list', params, (json) => {
            question_list = json.question_list  
//            $page  = _page
            total = json.total
            kw = $keyword
//            consol.log(total)
//          print(total)
        }) 
    }

//    get_question_list()
/*
이건 여러 줄 주석입니다
여러 줄 설명할 때 사용
*/
  $:$page, $keyword, get_question_list()
</script>

<div class="container my-3">
    <div class="row my3">
        <div class="col-6">
            <a use:link href="/open-api"  class="btn btn-primary">OpenAPI</a>
            <a use:link href="/question-create"  class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a>
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text"  class="form-control" bind:value="{kw}">
                <button class="btn btn-outline-secondary" on:click={() => {$keyword= kw, $page=0}}>
                  찾기
                </button>
            </div>
        </div>
    </div>
    <table class="table">
        <thead>
        <tr class="text-center table-dark">
            <th>번호</th>
            <th style="width:50%">제목</th>
            <th>글쓴이</th>            
            <th>작성일자</th>
        </tr>
        </thead>
        <tbody>
        {#each question_list as question, i}
        <tr class="text-center">
            <td>{ total-($page*size)-i}</td>
            <td class="text-start">
              <a use:link href="/detail/{question.id}">{question.subject}</a>
              {#if question.answers.length > 0}
              <span class="text-danger small mx-2">{question.answers.length}</span>
              {/if}
            </td>
            <!-- 날짜 주석 처리  
            <td>{question.create_date}</td>
            -->            
            <td>{question.user ? question.user.username : "" }</td>            
            <td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
        </tr>
        {/each}
        </tbody>
    </table>
    <!-- 페이징 처리 시작 -->
    <u1 class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => $page--}">이전</button>
        </li>
        <!-- 페이지번호 -->
        {#each Array(total_page) as _, loop_page}
        {#if loop_page >= $page-5 && loop_page <= $page+5}
            <li class="page-item {loop_page === $page && 'active'}">
                <button class="page-link" on:click="{() => $page=loop_page}">{loop_page+1}</button>
            </li>
        {/if}
        {/each}
        <!-- 다음페이지 -->
        <li class="page-item {$page >= total_page-1 && 'disabled'}">
            <button class="page-link" on:click="{() => $page++}">다음</button>
        </li>
    </u1>
    <!-- 페이징 처리 끝 -->
</div>