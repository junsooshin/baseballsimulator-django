from django import forms

class FormAway(forms.Form):
  batterAway1 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 1'}))
  batterAway2 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 2'}))
  batterAway3 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 3'}))
  batterAway4 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 4'}))
  batterAway5 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 5'}))
  batterAway6 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 6'}))
  batterAway7 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 7'}))
  batterAway8 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 8'}))
  batterAway9 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 9'}))
  pitcherAway = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Pitcher'}))

class FormHome(forms.Form):
  batterHome1 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 1'}))
  batterHome2 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 2'}))
  batterHome3 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 3'}))
  batterHome4 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 4'}))
  batterHome5 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 5'}))
  batterHome6 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 6'}))
  batterHome7 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 7'}))
  batterHome8 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 8'}))
  batterHome9 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Batter 9'}))
  pitcherHome = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Pitcher'}))