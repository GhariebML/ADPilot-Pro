import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { CampaignBriefForm } from '../../components/CampaignBriefForm'
import { campaignService } from '../../services/api'

describe('CampaignBriefForm', () => {
  it('renders form with all required fields', () => {
    const mockSubmit = vi.fn()
    render(<CampaignBriefForm onSubmit={mockSubmit} />)

    expect(screen.getByText('1-Click Vertical Presets')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('e.g. VisionGuard AI')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('e.g. Enterprise Security Platform')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Describe key features, primary differentiators, and value proposition...')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('e.g. CISOs, VP of IT Security, Enterprise Operations Directors')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Launch 18-Stage Autonomous Pipeline/i })).toBeInTheDocument()
  })

  it('validates required fields', async () => {
    const user = userEvent.setup()
    const mockSubmit = vi.fn()
    render(<CampaignBriefForm onSubmit={mockSubmit} />)

    const submitButton = screen.getByRole('button', { name: /Launch 18-Stage Autonomous Pipeline/i })
    await user.click(submitButton)

    // wait for form validation to prevent submission
    await waitFor(() => {
      expect(mockSubmit).not.toHaveBeenCalled()
    })
  })

  it('submits form with valid data', async () => {
    const user = userEvent.setup()
    const mockSubmit = vi.fn()
    vi.spyOn(campaignService, 'submitCampaign').mockResolvedValueOnce({ taskId: 'task-test-123' })
    render(<CampaignBriefForm onSubmit={mockSubmit} />)

    const businessInput = screen.getByPlaceholderText('e.g. VisionGuard AI')
    const productInput = screen.getByPlaceholderText('e.g. Enterprise Security Platform')
    const descInput = screen.getByPlaceholderText('Describe key features, primary differentiators, and value proposition...')
    const audienceInput = screen.getByPlaceholderText('e.g. CISOs, VP of IT Security, Enterprise Operations Directors')
    const budgetInput = screen.getByPlaceholderText('10000')

    await user.type(businessInput, 'Test Business')
    await user.type(productInput, 'Test Product')
    await user.type(descInput, 'A great product with autonomous AI capabilities.')
    await user.type(audienceInput, 'Young professionals and founders')
    await user.clear(budgetInput)
    await user.type(budgetInput, '5000')

    const submitButton = screen.getByRole('button', { name: /Launch 18-Stage Autonomous Pipeline/i })
    await user.click(submitButton)

    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith('task-test-123')
    })
  })

  it('displays error message on submission failure', async () => {
    const user = userEvent.setup()
    const mockSubmit = vi.fn()
    vi.spyOn(campaignService, 'submitCampaign').mockRejectedValueOnce(new Error('API error occurred'))
    render(<CampaignBriefForm onSubmit={mockSubmit} />)

    const businessInput = screen.getByPlaceholderText('e.g. VisionGuard AI')
    const productInput = screen.getByPlaceholderText('e.g. Enterprise Security Platform')
    const descInput = screen.getByPlaceholderText('Describe key features, primary differentiators, and value proposition...')
    const audienceInput = screen.getByPlaceholderText('e.g. CISOs, VP of IT Security, Enterprise Operations Directors')
    const budgetInput = screen.getByPlaceholderText('10000')

    await user.type(businessInput, 'Test Business')
    await user.type(productInput, 'Test Product')
    await user.type(descInput, 'A great product with autonomous AI capabilities.')
    await user.type(audienceInput, 'Young professionals and founders')
    await user.clear(budgetInput)
    await user.type(budgetInput, '5000')

    const submitButton = screen.getByRole('button', { name: /Launch 18-Stage Autonomous Pipeline/i })
    await user.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/API error occurred/i)).toBeInTheDocument()
    })
  })

  it('disables submit button while loading', async () => {
    const mockSubmit = vi.fn()
    const { rerender } = render(<CampaignBriefForm onSubmit={mockSubmit} isLoading={false} />)

    let submitButton = screen.getByRole('button', { name: /Launch 18-Stage Autonomous Pipeline/i })
    expect(submitButton).not.toBeDisabled()

    rerender(<CampaignBriefForm onSubmit={mockSubmit} isLoading={true} />)

    const loadingButton = screen.getByRole('button', { name: /Orchestrating 18 AI Agents/i })
    expect(loadingButton).toBeDisabled()
  })
})
