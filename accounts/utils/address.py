import requests

def get_google_address(api_key, address):

  def get_component(name, addr_components):
    test = lambda item: name in item['types']
    return next(filter(test, addr_components), None)
  lat, lng = None, None
  assert api_key is not None, "GOOGLE_API_KEY not in app.config"
  base_url = "https://maps.googleapis.com/maps/api/geocode/json"
  endpoint = f"{base_url}?address={address}&key={api_key}"
  # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
  r = requests.get(endpoint)
  if r.status_code not in range(200, 299):
      return None, None
  try:
      results = r.json()['results'][0]
      lat = results['geometry']['location']['lat']
      lng = results['geometry']['location']['lng']
  except:
      pass
  comps = results['address_components']
  return {
    "line_1": f"{comps[0]['long_name']} {comps[1]['long_name']}",
    "city": get_component('locality', comps)['long_name'],
    "state": get_component('administrative_area_level_1', comps)['long_name'],
    "country": get_component('country', comps)['short_name'],
    "postal_code": get_component('postal_code', comps)['long_name'],
    "coordinates": [lng, lat]
  }