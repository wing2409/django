<head>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
  <link rel="stylesheet" href="starter-template.css">
</head>

<nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
  <a class="navbar-brand" href="#">NER TEST</a>
  </div>
</nav>
    <div class="jumbotron">
    <div class="container">
      <h1 class="display-3">NER Demo</h1>
      <p>분석을 원하시는 문장을 입력하시고 모델을 선택하시면 NER 분석 결과를 보실 수 있습니다.</p>
      <form action="{% url 'vote'%}" method="post">
        {% csrf_token %}
      <p><input class="form-control mr-sm-2" id="nerText" name="nerText" type="text" placeholder="입력문장"></p>
      <p><button class="btn btn-primary btn-lg mr-sm-2" type="submit">분석</button></p>
      </form>
    </div>
  </div>

<div class="container">
  <div class="card-deck mb-3 text-center">
    <div class="card mb-4 shadow-sm">
      <div class="card-header">
        <h4 class="my-0 font-weight-normal">분석 결과</h4>
      </div>
      <div class="card-body">
          <h3 class="card-title pricing-card-title">{{result.resultText}}</h3>
        <table>
        <thead>
            <tr>
                {% for test in result.resultList %}
                <th style="text-align: center">{{ test.0 }}</th>
                {% endfor %}
            </tr>
            <tr>
                {% for test in result.resultList %}
                  {% if test.1 == 'O' %}
                  <th style="text-align: center"><button class="btn btn-Secondary" style="width:70px;" >{{ test.1 }}</button></th>
                  {% else %}
                  <th style="text-align: center"><button class="btn btn-Success" style="width:70px;" >{{ test.1 }}</button></th>
                  {% endif %}
                {% endfor %}
            </tr>
        </thead>
        </table>
      </div>
    </div>
  </div>
</div>
<!--					<button type="button" class="btn btn-primary">Primary</button>
					<button type="button" class="btn btn-secondary">Secondary</button>
					<button type="button" class="btn btn-success">Success</button>
					<button type="button" class="btn btn-danger">Danger</button>
					<button type="button" class="btn btn-warning">Warning</button>
					<button type="button" class="btn btn-info">Info</button>
					<button type="button" class="btn btn-light">Light</button>
					<button type="button" class="btn btn-dark">Dark</button>
					<button type="button" class="btn btn-link">Link</button>-->
<!--  <div class="starter-template">
    <h1>Bootstrap starter template</h1>
    <form class="form-inline my-2 my-lg-0" action="{% url 'vote'%}" method="post">
      {% csrf_token %}
      <input class="form-control mr-sm-2" id="nerText" name="nerText" type="text" placeholder="입력문장">
      <button class="btn btn-secondary my-2 my-sm-0" type="submit">분석</button>

      &lt;!&ndash;<p><label for="title">결과 : </label><input type="text" id="title" name="title" value="{{ result}}"/></p>&ndash;&gt;

      <main role="main" class="container">
            <div class="starter-template">

              <input class="form-control mr-sm-2"  type="text" value="{{ result}}">
            </div>
      </main>
    </form>
  </div>-->

</main><!-- /.container -->










def vote(request):

    txt = request.POST['nerText']
    returnText = predict(txt)

    result = {'resultList' : returnText, 'resultText' : txt}

    return render(request, 'index.html', {'result': result})


