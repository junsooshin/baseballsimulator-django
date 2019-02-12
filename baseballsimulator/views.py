from django.views import generic
from baseballsimulator.forms import FormAway, FormHome
from django.shortcuts import render

from .models import Batter, Pitcher, League 
from baseballsimulator.custom.correct_player import check_names, get_correct_player
from baseballsimulator.custom.simulation import simulate

# display the form to fill out player names
def index(request):
  formAway = FormAway()
  formHome = FormHome()
  context = {
    'formAway': formAway,
    'formHome': formHome,
  }
  return render(request, 'baseballsimulator/index.html', context)

# check the player names - if successful, call results and if not, display
# the previous form with the error messages
def results(request):
  batterNamesAway = [request.GET.get('batterAway1'), 
             request.GET.get('batterAway2'),
             request.GET.get('batterAway3'),
             request.GET.get('batterAway4'),
             request.GET.get('batterAway5'),
             request.GET.get('batterAway6'),
             request.GET.get('batterAway7'),
             request.GET.get('batterAway8'),
             request.GET.get('batterAway9')]
  batterNamesHome = [request.GET.get('batterHome1'), 
             request.GET.get('batterHome2'),
             request.GET.get('batterHome3'),
             request.GET.get('batterHome4'),
             request.GET.get('batterHome5'),
             request.GET.get('batterHome6'),
             request.GET.get('batterHome7'),
             request.GET.get('batterHome8'),
             request.GET.get('batterHome9')]
  pitcherNameAway = request.GET.get('pitcherAway')
  pitcherNameHome = request.GET.get('pitcherHome')

  invalidNames = check_names(batterNamesAway, pitcherNameAway, batterNamesHome, pitcherNameHome)
  
  if invalidNames:
    formAway = FormAway(initial={'batterAway1': batterNamesAway[0],
                   'batterAway2': batterNamesAway[1],
                   'batterAway3': batterNamesAway[2],
                   'batterAway4': batterNamesAway[3],
                   'batterAway5': batterNamesAway[4],
                   'batterAway6': batterNamesAway[5],
                   'batterAway7': batterNamesAway[6],
                   'batterAway8': batterNamesAway[7],
                   'batterAway9': batterNamesAway[8],
                   'pitcherAway': pitcherNameAway})
    formHome = FormHome(initial={'batterHome1': batterNamesHome[0],
                   'batterHome2': batterNamesHome[1],
                   'batterHome3': batterNamesHome[2],
                   'batterHome4': batterNamesHome[3],
                   'batterHome5': batterNamesHome[4],
                   'batterHome6': batterNamesHome[5],
                   'batterHome7': batterNamesHome[6],
                   'batterHome8': batterNamesHome[7],
                   'batterHome9': batterNamesHome[8],
                   'pitcherHome': pitcherNameHome})
    context = {
      'formAway': formAway,
      'formHome': formHome,
      'invalidNames': invalidNames,
    }
    return render(request, 'baseballsimulator/index.html', context)
  else:
    batterListAway = []
    batterListHome = []
    for batterNameAway, batterNameHome in zip(batterNamesAway, batterNamesHome):
      batterListAway.append(get_correct_player(batterNameAway, 'batter'))
      batterListHome.append(get_correct_player(batterNameHome, 'batter'))
    pitcherAway = get_correct_player(pitcherNameAway, 'pitcher')
    pitcherHome = get_correct_player(pitcherNameHome, 'pitcher')
    league = League.objects.get(year=2017)
    result = simulate(500,
              batterListAway, pitcherAway, 
              batterListHome, pitcherHome,
              league)
    context = {
      'winningPercentageAway': result[0],
      'winningPercentageHome': result[1],
      'batterNamesAway': batterNamesAway,
      'batterNamesHome': batterNamesHome,
      'pitcherNameAway': pitcherNameAway,
      'pitcherNameHome': pitcherNameHome,
    }
    return render(request, 'baseballsimulator/results.html', context)
