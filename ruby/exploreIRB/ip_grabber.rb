require 'httparty'
class IPGrabber

  def initialize()
    @url = "http://icanhazip.com"
  end

  def get
    response = HTTParty.get(@url)
    response.body.chomp  # remove the \n if it exists
  end
end