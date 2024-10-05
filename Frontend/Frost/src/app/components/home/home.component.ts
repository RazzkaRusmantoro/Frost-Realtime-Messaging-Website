import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { trigger, transition, style, animate } from '@angular/animations';
import { CommonModule } from '@angular/common';
import { RouterModule, RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';




@Component({
  selector: 'app-home',
  standalone: true,
  imports: [FormsModule,RouterModule, CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  animations: [
    trigger('slideDown', [
      transition(':enter', [
        style({ transform: 'translateY(-100%)', opacity: 0 }),
        animate('0.5s ease', style({ transform: 'translateY(0)', opacity: 1 })),
      ]),
    ]),
  ],
})
export class HomeComponent {

}
