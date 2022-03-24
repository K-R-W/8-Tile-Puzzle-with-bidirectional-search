from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from .solver import solver
# Create your views here.

@api_view(['POST'])
def getData(request):
    # size=request.data.get("size",'')
    board=json.loads(request.data.get("board",''))
    print(board) # remove this later
    solve_obj = solver(board)
    directions = solve_obj.solve()
    return Response({'directions':json.dumps(directions)})
