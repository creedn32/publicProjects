RSpec.describe do
  it 'verifies that false is false' do
    expect(false).not_to be
  end

  it 'also verifies that false is false' do
    expect(false).to be(false)
  end

  it 'another verification that false is false' do
    expect(false).not_to be(true)
  end
end
