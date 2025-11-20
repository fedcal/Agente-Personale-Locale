import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AgentUi } from './agent-ui';

describe('AgentUi', () => {
  let component: AgentUi;
  let fixture: ComponentFixture<AgentUi>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AgentUi]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AgentUi);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
