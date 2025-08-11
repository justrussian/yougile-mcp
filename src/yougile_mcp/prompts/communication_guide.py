"""
MCP prompts for task communication and collaboration workflows.
Guides for using comments, chats, and team coordination features.
"""

from typing import List
from mcp.server.fastmcp.prompts import base


def task_communication_workflow_prompt() -> List[base.Message]:
    """
    Guide for effective task communication and collaboration.
    
    Returns:
        Conversation flow for task communication best practices
    """
    return [
        base.UserMessage("How should I communicate about task progress and collaborate with my team in YouGile?"),
        base.AssistantMessage("""I'll teach you effective task communication in YouGile! Here's a comprehensive approach:

**Key Principle**: Every task in YouGile has its own chat (task_id = chat_id). Use this for all task-related discussions.

## 1. Task Status Updates

**Regular Progress Updates:**
```python
# When starting work
add_task_comment(task_id="task-123", comment="🚀 Started working on user authentication. ETA: 2 days")

# During development
add_task_comment(task_id="task-123", comment="✅ API endpoints complete. Working on frontend integration now.")

# When blocked
add_task_comment(task_id="task-123", comment="⚠️ Blocked: Need design mockups for mobile responsive layout")

# When ready for review
add_task_comment(task_id="task-123", comment="🔍 Ready for code review. Please check PR #45")

# When complete
add_task_comment(task_id="task-123", comment="✅ Complete! Deployed to staging. Ready for QA testing.")
```

## 2. Team Coordination

**Subscribe Relevant Team Members:**
```python
# Add team members who need to follow task progress
update_task_chat_subscribers(
    task_id="task-123", 
    subscribers=["developer-1", "qa-lead", "product-manager"]
)

# Check who's subscribed
subscribers = get_task_chat_subscribers(task_id="task-123")
```

**Mention Specific People in Comments:**
```python
# Request input from specific team members
add_task_comment(
    task_id="task-123", 
    comment="@sarah-designer: Can you review the mobile layout? @mike-backend: API ready for integration"
)

# Ask questions
add_task_comment(
    task_id="task-123",
    comment="@product-owner: Should the search be case-sensitive? Need clarification on requirements."
)
```

## 3. Issue Reporting and Problem Solving

**Report Issues Clearly:**
```python
# Bug reports
add_task_comment(
    task_id="task-123",
    comment="🐛 Bug found: Login fails with special characters in password. Steps to reproduce: 1) Use password with @#$ 2) Click login 3) Gets 'Invalid format' error"
)

# Technical challenges
add_task_comment(
    task_id="task-123",
    comment="⚡ Performance issue: Search taking 3+ seconds with large datasets. Investigating indexing solutions."
)
```

Which aspect of task communication would you like to focus on first?"""),
        base.UserMessage("I want to learn how to effectively update task status and keep everyone informed."),
        base.AssistantMessage("""Perfect! Effective status updates are crucial for team coordination. Here's a proven system:

## Status Update Framework

### 1. **Start-of-Work Updates**
Always announce when you begin working:
```python
add_task_comment(
    task_id="task-123",
    comment="🚀 Starting work on user dashboard. Plan: 1) API integration 2) UI components 3) Testing. ETA: Thursday EOD"
)
```

### 2. **Progress Checkpoints** 
Update at 25%, 50%, 75% completion:
```python
# 25% - Foundation laid
add_task_comment(task_id="task-123", comment="25% ✅ Database schema and models complete")

# 50% - Major milestone  
add_task_comment(task_id="task-123", comment="50% ✅ API endpoints working. Starting frontend integration")

# 75% - Near completion
add_task_comment(task_id="task-123", comment="75% ✅ UI complete, running final tests. On track for Thursday")
```

### 3. **Blocker Alerts**
Immediately report anything that stops progress:
```python
add_task_comment(
    task_id="task-123",
    comment="🚨 BLOCKED: Waiting for API key from external service. @devops-team can you help expedite?"
)
```

### 4. **Handoff Communications**
When passing work to others:
```python
# Ready for review
add_task_comment(
    task_id="task-123",
    comment="🔍 Ready for code review @tech-lead. Key changes: authentication.py, user-dashboard.tsx. PR #67"
)

# Ready for testing
add_task_comment(
    task_id="task-123", 
    comment="🧪 Ready for QA @qa-team. Test user: demo@test.com/password123. Focus on mobile responsive behavior"
)
```

### 5. **Completion Confirmation**
Always announce task completion with key details:
```python
add_task_comment(
    task_id="task-123",
    comment="✅ COMPLETE: User dashboard deployed to production. New features: real-time updates, mobile responsive design. Documentation updated in Confluence."
)
```

## Pro Tips for Status Updates:

**Use Emojis for Visual Clarity:**
- 🚀 Starting work
- ✅ Milestone reached
- 🚨 Blocked/urgent
- 🔍 Ready for review
- 🧪 Ready for testing
- ⚠️ Issue/concern
- 💡 Idea/suggestion

**Include Context:**
- What was done
- What's next
- Any dependencies
- Specific people to notify
- Relevant links (PRs, docs, etc.)

**Set Expectations:**
- Realistic timelines
- What others can expect
- When you'll provide next update

Would you like to practice writing status updates for a specific task scenario?""")
    ]


def team_collaboration_prompt() -> str:
    """
    Guide for effective team collaboration using YouGile communication features.
    
    Returns:
        Comprehensive team collaboration guide
    """
    return """# Team Collaboration Guide for YouGile

Master team coordination and communication using YouGile's chat and task features.

## Core Collaboration Principles

### 1. **Task-Centric Communication**
Every discussion should happen in the relevant task chat:

```python
# ✅ Good: Discuss in task context
add_task_comment(task_id="auth-task", comment="Should we use JWT or session-based auth?")

# ❌ Avoid: Generic team chat for specific task issues
send_chat_message(chat_id="general-chat", message="How should auth work?")
```

### 2. **Subscription Management**
Keep the right people informed without overwhelming others:

```python
# Subscribe stakeholders to important tasks
update_task_chat_subscribers(
    task_id="critical-bug-fix",
    subscribers=["product-manager", "tech-lead", "customer-success"]
)

# Subscribe domain experts
update_task_chat_subscribers(
    task_id="payment-integration", 
    subscribers=["payments-specialist", "security-expert"]
)
```

### 3. **Clear Handoffs**
Use structured communication for work transitions:

```python
# Developer to QA handoff
add_task_comment(
    task_id="feature-x",
    comment='''🔄 HANDOFF TO QA @qa-team
    
**What's Ready:** User registration with email verification
**Test Environment:** staging.app.com
**Test Accounts:** test1@demo.com / test2@demo.com  
**Focus Areas:** Email delivery, validation errors, mobile UI
**Known Issues:** Minor styling issue on iPhone SE (logged separately)
**Timeline:** Please complete testing by Friday EOD for Monday release'''
)
```

## Team Communication Patterns

### Daily Standup Integration
Use task comments to prepare for standups:

```python
# What you did yesterday
add_task_comment(task_id="task-1", comment="Yesterday: Completed user authentication API")

# What you're doing today  
add_task_comment(task_id="task-2", comment="Today: Starting frontend integration")

# Any blockers
add_task_comment(task_id="task-3", comment="Blocked: Waiting for design approval")
```

### Code Review Workflow
Streamline code reviews with task integration:

```python
# Request review
add_task_comment(
    task_id="feature-123",
    comment="🔍 Code Review Requested @senior-dev. PR: #234. Focus: error handling and performance"
)

# Provide review feedback
add_task_comment(
    task_id="feature-123", 
    comment="Review complete ✅ LGTM! Minor suggestion: consider caching in user service. Ready to merge."
)
```

### Cross-Team Coordination
Manage dependencies between teams:

```python
# Frontend waiting for backend
add_task_comment(
    task_id="frontend-task",
    comment="⏸️ Paused: Waiting for API endpoints from @backend-team. ETA needed for endpoint completion."
)

# Backend providing update
add_task_comment(
    task_id="api-task",
    comment="📡 API Update for @frontend-team: User endpoints ready on staging. Auth endpoints coming tomorrow."
)
```

## Advanced Collaboration Features

### Group Chat for Strategic Discussions
Use group chats for broader team coordination:

```python
# Create focused team chats
sprint_chat = create_group_chat(
    title="Sprint 24 - Authentication",
    participants=["dev-team", "qa-team", "product-owner"],
    description="All discussions for authentication sprint"
)

# Daily coordination
send_chat_message(
    chat_id=sprint_chat["id"],
    message="🌅 Daily sync: Auth sprint 60% complete. No blockers. Demo ready for Friday."
)
```

### Documentation Integration
Link documentation in task comments:

```python
add_task_comment(
    task_id="api-integration",
    comment='''📚 Documentation Updated:
    - API specs: https://docs.company.com/api/auth
    - Setup guide: https://confluence.company.com/setup  
    - Test cases: https://testplan.company.com/auth
    
@team please review before implementation.'''
)
```

## Communication Best Practices

### 1. **Be Specific and Actionable**
```python
# ✅ Specific and actionable
add_task_comment(
    task_id="bug-fix",
    comment="Bug reproduced ✅ Root cause: null check missing in validateEmail() line 42. Fix incoming in 1 hour."
)

# ❌ Vague and unhelpful  
add_task_comment(task_id="bug-fix", comment="looking at it")
```

### 2. **Use Threading for Related Discussions**
Keep conversations organized by getting message history:

```python
# Get context before adding to discussion
recent_comments = get_task_comments(task_id="design-task", limit=10)
# Read through recent comments, then add contextual response
add_task_comment(
    task_id="design-task",
    comment="Following up on the color scheme discussion - I've tested the accessibility and contrast ratios meet WCAG standards ✅"
)
```

### 3. **Close Loops**
Always acknowledge receipt and completion:

```python
# Acknowledge requests
add_task_comment(task_id="task-123", comment="👍 Got it @product-manager. Will have mockups ready by Wednesday.")

# Confirm completion  
add_task_comment(task_id="task-123", comment="✅ Done @qa-team. Deployed to staging and ready for your testing.")
```

**Remember**: Good communication prevents more problems than good code fixes! 🎯

## Task Assignment and Ownership Management

### Creating Tasks with Assigned Users
Always assign tasks to the right people from the start:

```python
# Create task with multiple assignees
create_task(
    title="Implement user authentication",
    column_id="col-in-progress",
    description="Add JWT-based auth with social login options",
    assigned_users=["backend-dev-id", "frontend-dev-id"]  # Both backend and frontend devs
)

# Create task for specific team member
create_task(
    title="Design login mockups", 
    column_id="col-design",
    assigned_users=["ui-designer-id"]  # Single assignee
)
```

### Reassigning Tasks
Change task ownership as work progresses:

```python
# Reassign from developer to QA
update_task(
    task_id="task-123",
    assigned_users=["qa-engineer-id"]  # Move from dev to QA
)

# Add additional people (collaboration)
update_task(
    task_id="complex-task",
    assigned_users=["senior-dev", "junior-dev", "tech-lead"]  # Team effort
)

# Remove all assignees (make unassigned)
update_task(
    task_id="backlog-task",
    assigned_users=[]  # Back to unassigned pool
)
```

### Assignment Best Practices

**1. Clear Ownership**
```python
# ✅ Good: Single owner for accountability
create_task(
    title="Fix critical payment bug",
    column_id="col-urgent", 
    assigned_users=["payments-expert-id"]
)

# ❌ Avoid: Too many owners without clear responsibility
create_task(
    title="Fix critical bug",
    assigned_users=["dev1", "dev2", "dev3", "dev4"]  # Who's actually responsible?
)
```

**2. Handoff Communication**
```python
# When reassigning, communicate why
add_task_comment(
    task_id="task-123",
    comment="🔄 Reassigning to @qa-team. Development complete, ready for testing. Test cases in PR description."
)

# Update assignment
update_task(task_id="task-123", assigned_users=["qa-lead-id"])
```

**3. Team Assignment Patterns**
```python
# Research/Discovery tasks - Single expert
update_task(task_id="research-task", assigned_users=["senior-architect"])

# Implementation tasks - Pair or small team  
update_task(task_id="feature-task", assigned_users=["dev1", "dev2"])

# Review tasks - Multiple reviewers
update_task(task_id="critical-review", assigned_users=["tech-lead", "security-expert"])

# Cross-team tasks - Representatives from each team
update_task(task_id="integration-task", assigned_users=["backend-lead", "frontend-lead", "qa-lead"])
```

### Finding the Right People to Assign

**Get Team Members:**
```python
# Find available team members
all_users = list_users()
# Look through users to find the right skills/availability

# Filter by current workload
busy_users = list_tasks(assigned_to="user-id")  # Check how many tasks they have
```

**Assignment Workflow:**
```python
# 1. Find the right person
team_members = list_users()
# Review team_members list for skills match

# 2. Check their current workload  
current_tasks = list_tasks(assigned_to="potential-assignee-id")
print(f"Current workload: {len(current_tasks)} tasks")

# 3. Assign if capacity allows
if len(current_tasks) < 5:  # Reasonable workload
    update_task(task_id="new-task", assigned_users=["potential-assignee-id"])
    add_task_comment(task_id="new-task", comment="Assigned based on expertise and current capacity")
```

Clear assignment reduces confusion and ensures accountability! 🎯"""


def meeting_integration_prompt() -> List[base.Message]:
    """
    Guide for integrating YouGile task communication with team meetings.
    
    Returns:
        Meeting integration workflow
    """
    return [
        base.UserMessage("How can I integrate YouGile task communication with our team meetings and planning sessions?"),
        base.AssistantMessage("""Excellent question! Integrating YouGile communication with meetings creates seamless workflow continuity. Here's how:

## Pre-Meeting Preparation

### 1. **Standup Preparation**
Use task comments to prepare talking points:

```python
# Review tasks and add pre-standup summaries
add_task_comment(task_id="current-task", comment="📊 Standup prep: 80% complete, testing mobile layout, no blockers")

# Get discussion points from task history
recent_updates = get_task_comments(task_id="complex-task", limit=5)
# Review recent comments to identify discussion points
```

### 2. **Sprint Planning Integration**
Gather task insights for planning:

```python
# Document task complexity insights
add_task_comment(
    task_id="completed-task",
    comment="📈 Retrospective note: This task took 2x expected time due to API changes. Factor similar complexity for future estimates."
)

# Capture dependencies for planning
add_task_comment(
    task_id="upcoming-task",
    comment="🔗 Planning note: Depends on design system completion. Should be scheduled after task-456."
)
```

## During Meetings

### 3. **Live Meeting Documentation**
Capture meeting decisions directly in task comments:

```python
# Record decisions made in meetings
add_task_comment(
    task_id="architecture-decision",
    comment='''📋 Architecture Meeting Decisions (Nov 15):
    - Use PostgreSQL over MongoDB for user data
    - Implement Redis for session caching  
    - Target: 10k concurrent users
    - @backend-team to create POC by Friday
    
    Present: @tech-lead @senior-dev @product-manager'''
)

# Action items from meetings
add_task_comment(
    task_id="new-feature",
    comment="🎯 Action Item from Product Meeting: Add user analytics tracking. @data-team to define events. Due: End of sprint."
)
```

### 4. **Real-time Status Updates**
Update task status during standups:

```python
# Quick status updates during standup
add_task_comment(task_id="current-work", comment="📍 Standup update: Moving to testing phase. ETA unchanged - Friday.")

# Address blockers mentioned in standup
add_task_comment(task_id="blocked-task", comment="🔓 Blocker resolved in standup: @devops provided API keys. Resuming development.")
```

## Post-Meeting Follow-up

### 5. **Meeting Outcomes Documentation**
Translate meeting outcomes to actionable task updates:

```python
# Sprint retrospective insights
add_task_comment(
    task_id="process-improvement",
    comment='''🔄 Retro Actions from Sprint 23:
    - Start code reviews earlier in development
    - Add automated testing for API endpoints  
    - Schedule mid-sprint check-ins for complex tasks
    - @team-lead to implement by next sprint'''
)

# Planning meeting decisions
add_task_comment(
    task_id="next-sprint-features", 
    comment='''📅 Sprint 24 Planning Decisions:
    - Priority: User authentication (5 points)
    - Secondary: Profile management (3 points)
    - Stretch: Social login integration (2 points)
    - @frontend-team focus on auth UI, @backend-team on security'''
)
```

### 6. **Async Follow-up Communications**
Continue meeting discussions in task context:

```python
# Follow up on meeting questions
add_task_comment(
    task_id="database-migration",
    comment="Following up on our architecture meeting question: Migration scripts are ready. Estimated downtime: 15 minutes during off-peak hours."
)

# Share additional resources discussed
add_task_comment(
    task_id="performance-optimization",
    comment='''📚 Resources from our performance discussion:
    - Profiling tool: https://tool.com  
    - Best practices doc: https://docs.com/perf
    - Benchmark results: attached to this task
    
    Let's implement these patterns in the current sprint.'''
)
```

## Meeting-Task Workflow Patterns

### **Pattern 1: Meeting → Task Creation**
```python
# Create tasks from meeting discussions
new_task = create_task(
    title="Implement Redis Caching (from Architecture Meeting)",
    column_id="backlog-column",
    description="Implement Redis for session and user data caching as decided in Nov 15 architecture meeting"
)

# Link meeting context
add_task_comment(
    task_id=new_task["id"],
    comment="📋 Created from Architecture Meeting (Nov 15). Decision rationale: Improve response times for user profiles. Target: 50% faster loads."
)
```

### **Pattern 2: Task → Meeting Agenda**
```python
# Prepare meeting agendas from task issues
blockers = get_task_comments(task_id="blocked-task", limit=10)
# Use blocker comments to create meeting agenda items

add_task_comment(
    task_id="meeting-prep",
    comment="📋 Friday Meeting Agenda: 1) Resolve API authentication blocker 2) Review mobile testing results 3) Plan integration tasks"
)
```

This integration ensures that meetings and task work stay connected, creating a continuous flow of information and decision-making!

Would you like to focus on any specific meeting type (standups, planning, reviews) for more detailed guidance?""")
    ]